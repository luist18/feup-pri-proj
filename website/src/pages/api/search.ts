// Next.js API route support: https://nextjs.org/docs/api-routes/introduction
import type { NextApiRequest, NextApiResponse } from 'next'

import type {
  QueryReply,
  QueryDocument,
  SolrArticleDocument,
  SolrResponse,
} from 'types/solr'

import { solrURL } from 'config'
import axios from 'config/axios'

const DOCUMENTS_PER_PAGE = 20

type ErrorResponse = {
  error: string
}

async function get(
  req: NextApiRequest,
  res: NextApiResponse<QueryReply | ErrorResponse>
) {
  let { query } = req.body

  if (query.length === 0) query = '*:*'

  const { page = 1 } = req.body

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
      page,
      start,
      count,
      data: parsedDocs,
    }

    res.status(200).json(reply)
  } catch (err: any) {
    res.status(500).json({ error: err.message })
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
