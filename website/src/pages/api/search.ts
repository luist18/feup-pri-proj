// Next.js API route support: https://nextjs.org/docs/api-routes/introduction
import type { NextApiRequest, NextApiResponse } from 'next'
import fetch from 'node-fetch'

import { solrURL } from 'config'

type Data = {
  data: any
}

type ErrorResponse = {
  error: string
}

async function handleGet(
  req: NextApiRequest,
  res: NextApiResponse<Data | ErrorResponse>
) {
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

  try {
    const request = await fetch(`http://localhost${  solrURL}`, { method: 'GET', body: JSON.stringify(content) })

    const data = await request.json()

    res.status(200).json({ data })
  } catch (err : any) {
    res.status(500).json({ error: err })
  }  
}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<Data | ErrorResponse>
) {
  const { method } = req

  switch (method) {
    case 'GET':
      handleGet(req, res)
      break
    default:
      res.setHeader('Allow', ['GET'])
      res.status(405).end(`Method ${method} Not Allowed`)
  }
}
