import React, { ReactElement, ReactNode, useContext, useMemo, useState } from 'react'

type SearchContextProps = {
  search?: string,
  setSearch?: any,
}

const SearchContext = React.createContext<SearchContextProps>({})

type Props = {
  children?: ReactNode
}

const defaultProps: Props = {
  children: undefined
}

// eslint-disable-next-line react-hooks/rules-of-hooks
export const useSearch = useContext<SearchContextProps>(SearchContext)

export default function SearchProvider({children}: Props): ReactElement {
  const [search, setSearch] = useState<string>('')

  const searchValue = useMemo(() => ({search, setSearch}), [search])

  return (
    <SearchContext.Provider value = {searchValue}>
      {children}
    </SearchContext.Provider>
  )
}

SearchProvider.defaultProps = defaultProps