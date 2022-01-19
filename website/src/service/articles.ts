import { solrURL, DOCUMENTS_PER_PAGE } from 'config'
import axios from 'config/axios'
import type {
  QueryReply,
  QueryDocument,
  SolrArticleDocument,
  SolrResponse,
} from 'types/solr'

export async function fetchArticles(query = '*:*', page = 1) {
  const content = {
    params: {
      defType: 'edismax',
      qf: 'title_raw^3 title^2 text_raw^1.5 text^1 path^0.5 book^0.25',
      bq: 'state:Consolidado^4',
      pf: 'title_raw^3 title^2 text_raw^1.5 text^1 path^0.5 book^0.25',
      start: DOCUMENTS_PER_PAGE * (page - 1),
    },
    limit: DOCUMENTS_PER_PAGE,
    query,
  }

  const request = await axios.get(`http://solr:8983${solrURL}`, {
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Content-Type': 'application/json',
    },
    data: content,
  })

  const { data }: { data: SolrResponse } = request

  const count = data.response.numFound
  const { start } = data.response
  const { docs } = data.response

  const parsedDocs: QueryDocument[] = docs.map((doc: SolrArticleDocument) => ({
    book: doc.book,
    bookUrl: doc.book_url,
    date: doc.date,
    key: doc.key,
    path: doc.path,
    presidentName: doc.president_name,
    presidentParty: doc.president_party,
    state: doc.state,
    text: doc.text,
    title: doc.title,
    id: doc.id,
  }))

  const reply: QueryReply = {
    count,
    data: parsedDocs,
    page,
    query,
    start: start + 1,
  }

  return reply
}
