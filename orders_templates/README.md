# Template of a batch of orders

The file `example_batch.json` can be used as a template to craft your batch of orders.
After starting the server with `poetry run start_server` you can post your batch to the orderbook with

```@console
curl -X POST "http://127.0.0.1:8000/batches" -H "Content-Type: application/json" -d @example_batch.json
```
