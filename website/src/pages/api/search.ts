// Next.js API route support: https://nextjs.org/docs/api-routes/introduction
import type { NextApiRequest, NextApiResponse } from 'next'

import { solrURL, DOCUMENTS_PER_PAGE } from 'config'
import axios from 'config/axios'
import type {
  QueryReply,
  QueryDocument,
  SolrArticleDocument,
  SolrResponse,
} from 'types/solr'

type ErrorResponse = {
  error: string
}

async function get(
  req: NextApiRequest,
  res: NextApiResponse<QueryReply | ErrorResponse>
) {
  const { query: queryParam = '*:*' } = req.query

  let query = Array.isArray(queryParam) ? queryParam.join(' ') : queryParam
  query = query.trim().length === 0 ? '*:*' : query.trim()

  const { page: pageRaw = '1' } = req.query

  let page: number
  try {
    page = parseInt(pageRaw as string, 10)
  } catch (err) {
    page = 1
  }

  if (page < 1) {
    res.status(400).json({ error: 'Page must be greater or equal than 1' })
    return
  }

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

  try {
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

    const parsedDocs: QueryDocument[] = docs.map(
      (doc: SolrArticleDocument) => ({
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
      })
    )

    const reply: QueryReply = {
      count,
      data: parsedDocs,
      page,
      query,
      start: start + 1,
    }

    res.status(200).json(reply)
  } catch (err) {
    if (err instanceof Error) {
      res.status(500).json({ error: err.message })
    }
  }
}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<QueryReply | ErrorResponse>
) {
  const { method } = req

  switch (method) {
    case 'GET':
      get(req, res)
      break
    default:
      res.setHeader('Allow', ['GET'])
      res.status(405).end(`Method ${method} Not Allowed`)
  }
}
