

export const DAYS_OF_WEEK = [
  'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'
]

export function getPeriodicityLabel({ frequency, time, dow }) {
  if (frequency === '3x_per_day') {
    return 'Daily at 6:00, 12:00 and 18:00'
  }
  if (frequency === '6x_per_day') {
    return 'Daily at 6:00, 9:00, 12:00, 15:00, 18:00 and 21:00'
  }
  if (frequency === 'daily') {
    return `Daily at ${time}`
  }
  if (frequency === 'weekly') {
    return `Every ${DAYS_OF_WEEK[dow -1]} at ${time}`
  }
}
