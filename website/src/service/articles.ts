import { solrURL, DOCUMENTS_PER_PAGE } from 'config'
import axios from 'config/axios'
import type {
  QueryReply,
  QueryDocument,
  SolrArticleDocument,
  SolrResponse,
} from 'types/solr'

const queryMetrics = {
  qf: {
    book: 38.92432103822159,
    key: 61.56994575348722,
    path: 7.058582346255768,
    text: 2.4731813053938483,
    text_raw: 7.229762219930129,
    title: 9.425539065132167,
    title_raw: 0.39651608022263407,
  },
  pf: {
    book: 22.488846194363205,
    key: 0.9374478542140957,
    path: 22.387246976224922,
    text: 3.0407590739988253,
    text_raw: 17.2687750652928,
    title: 10.148322926042312,
    title_raw: 25.311744954858113,
  },
  consolidado: 30.0,
  tie: 0.2897121725263928,
}

export async function fetchArticles(query = '*:*', page = 1) {
  const params = {
    defType: 'edismax',
    qf: `book^${queryMetrics.qf.book} key^${queryMetrics.qf.key} path^${queryMetrics.qf.path} text^${queryMetrics.qf.text} text_raw^${queryMetrics.qf.text_raw} title^${queryMetrics.qf.title} title_raw^${queryMetrics.qf.title_raw}`,
    pf: `book^${queryMetrics.pf.book} key^${queryMetrics.pf.key} path^${queryMetrics.pf.path} text^${queryMetrics.pf.text} text_raw^${queryMetrics.pf.text_raw} title^${queryMetrics.pf.title} title_raw^${queryMetrics.pf.title_raw}`,
    bq: `state:Consolidado^${queryMetrics.consolidado}`,
    tie: `${queryMetrics.tie}`,
    q: query,
    start: (page - 1) * DOCUMENTS_PER_PAGE,
  }

  const content = {
    params,
    limit: DOCUMENTS_PER_PAGE,
  }

  console.log(content)

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

export async function fetchRelated(document: QueryDocument) {
  const content = {
    query: `+key:"art ${document.key}" +book_url:"${document.bookUrl}" -id:${
      document.id
    } +path:(${document.path.map((value) => `"+${value}"`).join(' ')})`,
    params: {
      debugQuery: true,
      defType: 'edismax',
    },
  }

  const request = await axios.get(`http://solr:8983${solrURL}`, {
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Content-Type': 'application/json',
    },
    data: content,
  })

  const { data }: { data: SolrResponse } = request

  const { docs } = data.response

  const parsedDocs: QueryDocument[] = docs.map((doc: SolrArticleDocument) => ({
    book: doc.book,
    bookUrl: doc.book_url,
    date: doc.date,
    key: doc.key,
    path: doc.path,
    presidentName: doc.president_name || null,
    presidentParty: doc.president_party || null,
    state: doc.state,
    text: doc.text,
    title: doc.title,
    id: doc.id,
  }))

  return parsedDocs
}

export async function fetchArticle(id: string) {
  const content = {
    limit: 1,
    query: `id:${id}`,
  }

  const request = await axios.get(`http://solr:8983${solrURL}`, {
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Content-Type': 'application/json',
    },
    data: content,
  })

  const { data }: { data: SolrResponse } = request

  const { docs } = data.response

  const parsedDocs: QueryDocument[] = docs.map((doc: SolrArticleDocument) => ({
    book: doc.book,
    bookUrl: doc.book_url,
    date: doc.date,
    key: doc.key,
    path: doc.path,
    presidentName: doc.president_name || null,
    presidentParty: doc.president_party || null,
    state: doc.state,
    text: doc.text,
    title: doc.title,
    id: doc.id,
  }))

  const doc = parsedDocs[0] || undefined

  if (doc === undefined) {
    return {
      article: undefined,
      related: [],
    }
  }

  const related = await fetchRelated(doc)

  return {
    article: doc,
    related,
  }
}
