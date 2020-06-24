from config import API_TOKEN
from dblighter import DbLighter
from parser_news import Parser

from aiogram import Bot, Dispatcher, executor, types
import logging
import uvloop
import asyncio


"""Configure logging"""
logging.basicConfig(level=logging.INFO)

"""Initialize bot and dispatcher"""
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

db = DbLighter()
np = Parser('l_key.txt')

@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.Message):
    if not db.subscriber_exist(message.from_user.id):
        db.add_subscriber(message.from_user.id)
    else:
        db.update_subscription(message.from_user.id)
	
    await message.answer('You are success subscribed!')

@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.Message):
    if not db.subscriber_exist(message.from_user.id):
        db.add_subscriber(message.from_user.id, False)
    else:
        db.update_subscription(message.from_user.id, False)

    await message.answer('You are success unsubsribed!')

async def scheduled(wait_for):
	while True:
		await asyncio.sleep(wait_for)

		new_posts = np.new_posts()

		if(new_posts):
			new_posts.reverse()
			for ng in new_posts:
				nfo = np.post_info(ng)

				subscriptions = db.get_subscriptions()

				with open(np.download_image(nfo["image"]), 'rb') as photo:
					for s in subscriptions:
						await bot.send_photo(
							s[1],
							photo,
							caption = nfo['title'] + "\n" + nfo['excerpt'] + "\n\n" + nfo['link'],
							disable_notification = True
						)
				
				np.update_lastkey(nfo['id'])


if __name__ == '__main__':
	uvloop.install()
	dp.loop.create_task(scheduled(60))
	executor.start_polling(dp, skip_updates=True)
