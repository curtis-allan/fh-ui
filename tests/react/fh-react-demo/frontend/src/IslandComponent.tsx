// components/src/IslandComponent.tsx
import * as React from 'react'
import JsxParser from 'react-jsx-parser'
import * as Components from '@/components'

interface IslandProps {
  jsxString: string
  bindings?: Record<string, any>
}

const IslandComponent: React.FC<IslandProps> = ({
  jsxString,
  bindings = {}
}) => {
  return (
    <JsxParser
      bindings={{
        ...bindings,
        ...Components
      }}
      components={Components}
      jsx={jsxString}
      renderInWrapper={false}
      showWarnings={true}
    />
  )
}

export default IslandComponent
