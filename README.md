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
      "Indulge in Frozen Delights: Discover the Story Behind Our Chilled Creations"
    ],
    "description": [
      "Welcome to our extraordinary ice cream shop, where every scoop is a delightful masterpiece. Indulge your taste buds in a world of delectable flavors crafted with the finest ingredients and a sprinkle of magic. Our passion for creating frozen delights knows no bounds, as we constantly push the boundaries of conventional ice cream. From classic favorites to innovative creations, we offer an extensive selection to satisfy any craving. Whether you're seeking a nostalgic treat or a bold new adventure, our ice cream shop promises to transport you to a place of unparalleled sweetness and joy. Come and experience the blissful world of ice cream perfection."
    ]
  },
  "refund": {
    "title": [
      "Sweet Satisfaction Guaranteed: Ice Cream Shop Refunds Made Easy!"
    ],
    "description": [
      "Welcome to our ice cream shop's refund page! We believe in serving pure happiness with every scoop, but if your experience falls short of expectations, we're here to make it right. Our refund policy is as sweet as our tantalizing flavors. Whether you didn't get the exact flavor you were craving or encountered any issues, simply reach out to our friendly customer support team. With their expert assistance, we'll ensure your satisfaction is restored. Your delight is our top priority, because every customer deserves an ice cream experience that's as delightful as can be."
    ]
  }
}
```
