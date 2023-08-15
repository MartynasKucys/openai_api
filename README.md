# Open ai api

In this repo there is an flask api that calls open ai gpt-3.5-turbo and rephrases or generated text. Due to the fact that
there can be a lot of section to the generate api call all section in parallel.

## How to launch

Build docker image

```bash
docker build -t openai_api .
```

After run the image

```bash
docker run -p 5000:5000 openai_api
```

This will run the flask api on localhost:5000.

There is also an .env file with "openai_key" that is your open ai api key and "api_key" that is the key for this api (by default "api_key")

## Using the api

### The /Rephrase api

It expects json with text and number of variants that you want to rephrase. </br>
example json.

```json
{ "text": "some text to rephrase", "number_of_variants": 2 }
```

You can call this function with programs like postman or curl. You can use this curl command.

```bash
curl -X GET http://localhost:5000/Rephrase -H "Content-Type: application/json" -H "Authorization: Bearer api_key" --data "{\"text\": \"This product is very very good \", \"number_of_variants\":2}"
```

It will return:

```json
["This product is extremely excellent.", "This product is excellent."]
```

### the /Generate api

It expects description about the company and then sections about what pages and what inside thous page to generate.

```json
{
  "description": "company description",
  "sections": {
    "about": { "title": 1, "description": 2 },
    "refund": { "title": 2, "description": 1 },
    "hero": { "title": 1, "description": 1 }
  }
}
```

The number represent how many variations of that this it should generate. </br>
For example if you pass this json

```json
{
  "description": "An ice cream shop",
  "sections": {
    "about": { "title": 2, "description": 1 },
    "refund": { "title": 1, "description": 1 }
  }
}
```

With this curl command:

```bash
curl -X GET http://localhost:5000/Generate -H "Content-Type: application/json" -H "Authorization: Bearer api_key" --data "{\"description\": \"An ice cream shop \", \"sections\":{ \"about\": {\"title\":2, \"description\":1}, \"refund\":{\"title\":1, \"description\":1} } } "

```

It returns:

```json
{"about": {"title": ["Indulge in Frozen Delights: Experience the Ultimate Ice Cream Haven"], "description": ["Welcome to our extraordinary ice cream shop, where every scoop is a delightfully decadent experience. Indulge your senses in our handcrafted, artisanal ice creams that are made with love and care. Our luscious flavors range from classic favorites like creamy vanilla bean and rich chocolate, to tantalizing creations such as salted caramel swirl and refreshing berry blast. We source only the finest ingredients to ensure each bite is a burst of pure bliss. Whether you're celebrating a special occasion or simply satisfying your sweet tooth, our ice cream shop is the ultimate destination for pure frozen enchantment. Explore a world of sweet sensations with us today!"]}, "refund": {"title": ["Chill Out and Refund \u2013 Satisfying Your
Sweet Tooth, One Scoop at a Time!"], "description": ["Welcome to our Ice Cream Shop's refund page! We genuinely believe that our delicious ice cream will delight your taste buds, but we understand that sometimes mistakes happen or preferences change. If you are unsatisfied, don't worry, we've got you covered. Our refund policy ensures your satisfaction is our top priority. Whether you accidentally ordered the wrong flavor or simply changed your mind, we'll gladly assist you with a hassle-free refund. Our dedicated customer support team is here to make sure you leave with a smile on your face and a satisfied palate. Your happiness and enjoyment are what we strive for, and we can't wait to serve you again soon!"]}}
```
