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
{
  "about": {
    "title": [
      "The Scoop: Discover Our Delicious Frozen Creations and Sweet Indulgences",
      "Indulge in Blissful Delights: Unveiling the Frosty Delights of Our Artisanal Ice Cream Shop"
    ],
    "description": [
      "Welcome to our delightful ice cream haven! Our ice cream shop is a dreamy paradise for all ice cream enthusiasts. Indulge in our handcrafted frozen treats that will transport your taste buds to a world of pure bliss. Each scoop is made with love and passion, using only the finest ingredients, ensuring the smoothest, creamiest ice cream experience. From classic flavors to exotic creations, there's something to satisfy every craving. With our charming ambiance and friendly service, we aim to create unforgettable moments and spread joy one scoop at a time. Come and join us for a delightful journey through the wonders of ice cream."
    ]
  },
  "refund": {
    "title": [
      "Sweet Satisfaction Guaranteed: Our Hassle-Free Ice Cream Refund Policy"
    ],
    "description": [
      "Welcome to our ice cream shop's refund page, where your satisfaction is our top priority! We understand that sometimes things don't go as planned, and we're here to make it right. If you're not 100% satisfied with your ice cream experience, we offer a hassle-free refund process. Simply reach out to our friendly team within [X] days of your purchase, and we'll gladly assist you. Whether it's an issue with the flavor, texture, or any other concern, we're committed to ensuring that every scoop brings a smile to your face. Your happiness is the cherry on top of our ice cream!"
    ]
  }
}
```
