import { useRouter } from 'next/router'

import React, { ReactElement } from 'react'

import { useSearch } from 'context/search'

import { Container } from './style'

export default function SearchBar(): ReactElement {
  const { search, setSearch, searchQuery } = useSearch()
  const router = useRouter()

  return (
    <Container>
      <form
        onSubmit={(event) => {
          event.preventDefault()
          searchQuery(search, 1)

          router.push(
            {
              pathname: '/',
              query: { q: search },
            },
            undefined,
            { shallow: true }
          )
        }}
      >
        <div className="relative">
          <span className="icon absolute h-full flex justify-center items-center p-3">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              x="0px"
              y="0px"
              width="26"
              height="26"
              viewBox="0 0 30 30"
              style={{ fill: 'var(--article-path)' }}
            >
              <path d="M 13 3 C 7.4889971 3 3 7.4889971 3 13 C 3 18.511003 7.4889971 23 13 23 C 15.396508 23 17.597385 22.148986 19.322266 20.736328 L 25.292969 26.707031 A 1.0001 1.0001 0 1 0 26.707031 25.292969 L 20.736328 19.322266 C 22.148986 17.597385 23 15.396508 23 13 C 23 7.4889971 18.511003 3 13 3 z M 13 5 C 17.430123 5 21 8.5698774 21 13 C 21 17.430123 17.430123 21 13 21 C 8.5698774 21 5 17.430123 5 13 C 5 8.5698774 8.5698774 5 13 5 z" />
            </svg>
          </span>
          <input
            className="bg-white py-3 px-6 text-lg rounded-2xl font-normal pl-14"
            style={{
              boxShadow: 'var(--article-box-shadow)',
            }}
            type="text"
            placeholder="Search"
            value={search}
            onChange={(event) => {
              const { value } = event.target
              setSearch(value)
            }}
          />
        </div>
      </form>
    </Container>
  )
}
