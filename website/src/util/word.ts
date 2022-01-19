export const capitalize = (word: string): string => {
  const lowercase = word.toLowerCase()
  return lowercase.charAt(0).toUpperCase() + lowercase.slice(1)
}

export function numberWithSpaces(number: number): string {
  return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ' ')
}
