import React, {
  ReactElement,
  ReactNode,
  useContext,
  useMemo,
  useReducer,
  useState,
} from 'react'

import axios from 'config/axios'
import { SearchState } from 'types/searchstate'
import { QueryReply } from 'types/solr'

import SearchReducer, { initialState } from './reducer'

type SearchContextProps = {
  search: string
  // eslint-disable-next-line no-unused-vars
  setSearch: (search: string) => void
  state: SearchState
  // eslint-disable-next-line no-unused-vars
  searchQuery: (query: string) => void
}

const SearchContext = React.createContext<SearchContextProps>({
  search: '',
  // eslint-disable-next-line @typescript-eslint/no-empty-function
  setSearch: () => {},
  state: initialState,
  // eslint-disable-next-line @typescript-eslint/no-empty-function
  searchQuery: () => {},
})

type Props = {
  children?: ReactNode
}

const defaultProps: Props = {
  children: undefined,
}

export const useSearch = () => useContext<SearchContextProps>(SearchContext)

export default function SearchProvider({ children }: Props): ReactElement {
  const [search, setSearch] = useState<string>('')
  const [state, dispatch] = useReducer(SearchReducer, initialState)

  const searchValue = useMemo(() => {
    async function searchQuery(query: string) {
      dispatch({ type: 'SEARCH_QUERY_REQUEST' })
      setSearch(query)

      const request = await axios.get('/api/search', {
        params: {
          query,
        },
      })

      if (request.status !== 200) {
        dispatch({ type: 'SEARCH_QUERY_FAILURE' })
        return
      }

      const { data }: { data: QueryReply } = request

      dispatch({ type: 'SEARCH_QUERY_SUCCESS', payload: data })
    }

    return {
      search,
      setSearch,
      state,
      searchQuery,
    }
  }, [search, state, dispatch])

  return (
    <SearchContext.Provider value={searchValue}>
      {children}
    </SearchContext.Provider>
  )
}

SearchProvider.defaultProps = defaultProps
