import React, { ReactElement } from 'react'

import { useSearch } from 'context/search'

import { Container } from './style'

export default function SearchBar(): ReactElement {
  const { search, setSearch, searchQuery } = useSearch()

  return (
    <Container>
      <form
        onSubmit={(event) => {
          event.preventDefault()
          searchQuery(search)
        }}
      >
        <input
          type="text"
          placeholder="Search"
          value={search}
          onChange={(event) => {
            const { value } = event.target
            setSearch(value)
          }}
        />
      </form>
    </Container>
  )
}
