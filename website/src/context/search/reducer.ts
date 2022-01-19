import { SearchState, SearchAction } from 'types/searchstate'

export const initialState: SearchState = {
  start: 1,
  page: 1,
  count: 0,
  results: [],
  loading: false,
  error: false,
}

export const reducer = (
  previousState: SearchState,
  action: SearchAction
): SearchState => {
  switch (action.type) {
    case 'SEARCH_QUERY_REQUEST':
      return { ...previousState, loading: true, error: false }
    case 'SEARCH_QUERY_SUCCESS':
      return {
        ...previousState,
        loading: false,
        results: action.payload.data,
        start: action.payload.start,
        count: action.payload.count,
        page: action.payload.page,
      }
    case 'SEARCH_QUERY_FAILURE':
      return { ...previousState, loading: false, error: true }
    default:
      throw new Error('Unhandled action type')
  }
}

export default reducer
