import styled from 'styled-components'

export const Container = styled.div`
  display: inline-grid;

  width: 100%;

  gap: 10px;
  grid-template-areas: 'filters results blank';
  grid-template-columns: auto 930px auto;
`
