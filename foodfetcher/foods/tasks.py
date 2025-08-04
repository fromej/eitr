from typing import List
from background_task import background
from openai import OpenAI
from pydantic import BaseModel
from django.conf import settings

from .models import FavoriteFoods

OPENAI_MODEL = "gpt-4.1-nano"

@background(schedule=0)
def get_favorite_foods(amount: int = 100):
    print(f"Starting to get {amount} favorite foods!")
    openai_client = OpenAI()

    class FavoriteFood(BaseModel):
        foods: List[str]
        vegitarian: bool

    all_responses = []

    for _ in range(amount):
        chat_a = openai_client.responses.create(
            model=OPENAI_MODEL,
            input="You are in a conversation with a true food lover. Ask him for his top three favorite foods."
        )

        chat_b = openai_client.responses.create(
        model=OPENAI_MODEL,
        input=chat_a.output_text,
        instructions="You are culinairy food lover that has a very diverse taste of foods. Randomly you feel like being vegan or vegitarian or a true meat lover.",
        temperature=1.3,
        )

        post_processing = openai_client.responses.parse(
            model=OPENAI_MODEL,
            input=chat_b.output_text,
            instructions="Extract the three favorite foods. Based on the favorite food determine if the user is vegitarian/vegan",
            text_format=FavoriteFood,
        )

        all_responses.append((
            chat_a.output_text, 
            chat_b.output_text, 
            post_processing.output_parsed
            ))

    food_responses = [
        FavoriteFoods(
            question=item[0], 
            answer=item[1], 
            foods=item[2].foods, 
            veggy=item[2].vegitarian) 
        for item in all_responses
    ]

    FavoriteFoods.objects.bulk_create(food_responses)

    print(f"Successfully inserted {len(food_responses)} records")