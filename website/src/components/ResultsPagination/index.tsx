/* eslint-disable jsx-a11y/anchor-is-valid */
/* This example requires Tailwind CSS v2.0+ */

interface Props {
  start: number
  count: number
  length: number
  onPrevious: () => void
  onNext: () => void
}

export default function ResultsPagination({
  start,
  count,
  length,
  onPrevious,
  onNext,
}: Props) {
  return (
    <div className="py-3 flex items-center justify-between">
      <div className="flex-1 flex items-center justify-between">
        <div>
          <p className="text-base app-dark-grey">
            A mostrar <span className="font-medium">{start}</span> até{' '}
            <span className="font-medium">{start + length - 1}</span> de{' '}
            <span className="font-medium">{count}</span> resultados
          </p>
        </div>
        <div>
          <nav
            className="relative z-0 inline-flex rounded-md shadow-sm space-x-2"
            aria-label="Pagination"
          >
            {start > 1 ? (
              <a
                href="#"
                className="relative inline-flex items-center px-2 py-2 rounded-md border border-gray-300 text-base font-medium app-dark-grey bg-white"
                onClick={(event) => {
                  event.preventDefault()
                  onPrevious()
                }}
              >
                <span className="app-dark-grey font-normal">Anterior</span>
                <span className="sr-only">Anterior</span>
              </a>
            ) : undefined}
            {start + length - 1 < count ? (
              <a
                href="#"
                className="relative inline-flex items-center px-2 py-2 rounded-md border border-gray-300 text-base font-medium app-dark-grey bg-white"
                onClick={(event) => {
                  event.preventDefault()
                  onNext()
                }}
              >
                <span className="app-dark-grey font-normal">Seguinte</span>
                <span className="sr-only">Seguinte</span>
              </a>
            ) : undefined}
          </nav>
        </div>
      </div>
    </div>
  )
}
