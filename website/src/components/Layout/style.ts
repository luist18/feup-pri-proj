import styled from 'styled-components'

export const Container = styled.div`
  display: inline-grid;

  width: 100%;

  gap: 10px;
  grid-template-areas: 'filters content blank';
  grid-template-columns: auto minmax(250px, 930px) auto;
`
