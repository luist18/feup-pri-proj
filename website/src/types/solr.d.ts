export type SolrArticleDocument = {
  book: string
  book_url: string
  date: Date
  key: string
  path: string[]
  president_name: string
  president_party: string
  state: string
  text: string
  title: string
  id: string
  _version_: number
}

export type SolrResponse = {
  responseHeader: {
    status: number
    QTime: number
    params: {
      json: string
    }
  }
  response: {
    numFound: number
    start: number
    docs: SolrArticleDocument[]
  }
}

export type QueryDocument = {
  book: string
  bookUrl: string
  date: Date
  key: string
  path: string[]
  presidentName: string
  presidentParty: string
  state: string
  text: string
  title: string
  id: string
}

export type QueryReply = {
  count: number
  data: QueryDocument[]
  page: number
  query: string
  start: number
}
