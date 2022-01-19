// Next.js API route support: https://nextjs.org/docs/api-routes/introduction
import type { NextApiRequest, NextApiResponse } from 'next'

import { fetchArticle } from 'service/articles'
import type { RelatedQueryReply } from 'types/solr'

type ErrorResponse = {
  error: string
}

async function get(
  req: NextApiRequest,
  res: NextApiResponse<RelatedQueryReply | ErrorResponse>
) {
  const { id } = req.query

  try {
    const reply = await fetchArticle(id.toString())

    res.status(200).json(reply)
  } catch (err) {
    if (err instanceof Error) {
      res.status(500).json({ error: err.message })
    }
  }
}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<RelatedQueryReply | ErrorResponse>
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
