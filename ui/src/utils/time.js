const timeFormatter = new Intl.DateTimeFormat('en-US', {
  hour: 'numeric',
  minute: '2-digit',
});

export function formatTime(date) {
  return timeFormatter.format(date);
}
