export function createMessage({ sender, content, time = new Date() }) {
  return {
    id: crypto.randomUUID(),
    sender,
    content,
    time,
  };
}

export function pickRandom(items) {
  return items[Math.floor(Math.random() * items.length)];
}
