import { QueryDocument, QueryReply } from './solr'

export type SearchState = {
  page: number
  count: number
  results: QueryDocument[]
  loading: boolean
  error: boolean
}

export type SearchAction =
  | { type: 'SET_QUERY'; query: string }
  | { type: 'SEARCH_QUERY_REQUEST' }
  | { type: 'SEARCH_QUERY_SUCCESS'; payload: QueryReply }
  | { type: 'SEARCH_QUERY_FAILURE' }
