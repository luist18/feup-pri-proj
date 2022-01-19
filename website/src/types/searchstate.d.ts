import { QueryDocument, QueryReply } from './solr'

export type SearchState = {
  page: number
  start: number
  count: number
  results: QueryDocument[]
  loading: boolean
  error: boolean
}

export type SearchAction =
  | { type: 'SEARCH_START'; payload: QueryReply }
  | { type: 'SEARCH_QUERY_REQUEST' }
  | { type: 'SEARCH_QUERY_SUCCESS'; payload: QueryReply }
  | { type: 'SEARCH_QUERY_FAILURE' }
