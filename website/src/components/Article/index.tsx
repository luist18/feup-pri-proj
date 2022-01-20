import { useRouter } from 'next/router'

import React, { useEffect } from 'react'

import moment from 'moment'
import 'moment/locale/pt'
import { QueryDocument } from 'types/solr'
import {
  capitalize,
  startsWithPoint,
  startsWithSubPoint,
  stateColor,
} from 'util/word'

import { Container } from './style'

type Props = {
  document: QueryDocument | undefined
  related: QueryDocument[]
}

export default function Article({ document, related }: Props) {
  const router = useRouter()

  useEffect(() => {
    if (!document) {
      router.push('/')
    }
  }, [])

  if (!document) {
    return <>Not found...</>
  }

  return (
    <Container className="mt-14">
      <header className="flex flex-col">
        <a
          href={`https://www.dre.pt${document.bookUrl}`}
          className="article-path text-xs mb-1"
        >
          {[document.book, ...document.path].join(' > ')}
        </a>
        <div className="flex items-center mb-2 flex-col sm:flex-row">
          <h2 className="text-xl font-normal article-title">{`Artigo ${document.key}º (${document.title})`}</h2>
          <span
            className="ml-auto h-full text-sm font-medium text-white py-1.5 px-3 rounded-xl"
            style={{
              backgroundColor: stateColor(document.state?.toLowerCase()),
            }}
          >
            {capitalize(document.state || 'Sem estado')}
          </span>
        </div>
      </header>
      <main className="my-3">
        {document.text.split('\\n').map((line) => (
          <p
            key={line.length * Math.random()}
            className={`article-text ${startsWithPoint(line) ? 'mt-3' : ''}`}
          >
            &emsp;{startsWithSubPoint(line) ? <>&emsp;</> : undefined}
            {line.trim()}
          </p>
        ))}
      </main>
      <footer className="flex flex-col">
        {document.presidentName && document.presidentParty ? (
          <span className="article-path text-sm">
            Sob a presidência de {document.presidentName} (
            {document.presidentParty})
          </span>
        ) : undefined}
        <span className="article-date ml-auto my-2">
          {moment(new Date(document.date))
            .locale('PT')
            .format('D [de] MMMM [de] YYYY')}
        </span>
      </footer>
      <div className="mt-4">
        <h2 className="text-lg font-normal article-title">
          Artigos relacionados
        </h2>
        <div>
          {related.length === 0 ? (
            <span className="article-path">Não há artigos relacionados</span>
          ) : (
            <div className="flex flex-col text-sm article-text">
              {related
                .sort(
                  (lhs, rhs) =>
                    new Date(rhs.date).getTime() - new Date(lhs.date).getTime()
                )
                .map((doc) => (
                  <a
                    key={doc.id}
                    href={`/artigo/${doc.id}`}
                    className="text-blue-700"
                  >{`Artigo ${doc.key}º (${doc.title}) [${capitalize(
                    doc.state
                  )}] - ${moment(new Date(doc.date))
                    .locale('PT')
                    .format('D [de] MMMM [de] YYYY')}`}</a>
                ))}
            </div>
          )}
        </div>
      </div>
    </Container>
  )
}
