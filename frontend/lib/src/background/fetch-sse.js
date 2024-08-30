import { streamAsyncIterable } from "./stream-async-iterable.js";

export async function fetchSSE(resource, options) {
  const { onMessage, onError, ...fetchOptions } = options;
  const resp = await fetch(resource, fetchOptions).catch((err) => onError(err));

  // stream processing
  for await (const chunk of streamAsyncIterable(resp.body)) {
    const message = new TextDecoder().decode(chunk);
    onMessage(message);
  }
}
