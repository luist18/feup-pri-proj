// Next.js API route support: https://nextjs.org/docs/api-routes/introduction
import type { NextApiRequest, NextApiResponse } from 'next'
import fetch from 'node-fetch'

import { solrURL } from 'config'
import { ServerResponse } from 'http'

type Data = {
  name: string
}

async function handleGet(req: NextApiRequest, res: NextApiResponse<Data>): Promise<ServerResponse> {
  const { query } = req.body

  const content = {
    params: {
      defType: 'edismax',
      qf: 'title_raw^3 title^2 text_raw^1.5 text^1 path^0.5 book^0.25',
      bq: 'state:Consolidado^4',
      pf: 'title_raw^3 title^2 text_raw^1.5 text^1 path^0.5 book^0.25',
    },
    query,
  }

  await fetch(solrURL, { method: 'GET', body: JSON.stringify(content) })

  return res.status(200).json({ name: 'John Doe' })
}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<Data>
) {
  if (req.method === 'GET') {
    const result = await handleGet(req, res)

    return result
  }
}
