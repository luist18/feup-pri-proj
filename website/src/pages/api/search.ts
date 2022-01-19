// Next.js API route support: https://nextjs.org/docs/api-routes/introduction
import type { NextApiRequest, NextApiResponse } from 'next'

import { fetchArticles } from 'service/articles'
import type { QueryReply } from 'types/solr'

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

  try {
    const reply = await fetchArticles(query, page)

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
      await get(req, res)
      break
    default:
      res.setHeader('Allow', ['GET'])
      res.status(405).end(`Method ${method} Not Allowed`)
  }
}
