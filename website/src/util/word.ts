export const capitalize = (word: string): string => {
  const lowercase = word.toLowerCase()
  return lowercase.charAt(0).toUpperCase() + lowercase.slice(1)
}

export function numberWithSpaces(number: number): string {
  return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ' ')
}

export function stateColor(state: string | undefined): string {
  switch (state) {
    case 'consolidado':
      return 'var(--article-state-green)'
    case 'alterado':
      return 'var(--article-state-yellow)'
    case 'revogado':
      return 'var(--article-state-red)'
    default:
      return 'var(--article-path)'
  }
}

export function startsWithPoint(line: string): boolean {
  return line.trim().match(/^\d\s?(-|.|\))\s/) !== null
}

export function startsWithSubPoint(line: string): boolean {
  return line.trim().match(/^\w\)\s/) !== null
}

// https://stackoverflow.com/questions/3446170/escape-string-for-use-in-javascript-regex
export function escapeRegExp(string: string) {
  return string.replace(/[.*+?^${}()|[\]\\]/g, '') // $& means the whole matched string
}
