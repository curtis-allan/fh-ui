import 'vite/modulepreload-polyfill'
import { createRoot } from 'react-dom/client'
import './index.css'
import IslandComponent from './IslandComponent'

function initializeIslands() {
  document.querySelectorAll('.react-island').forEach((island: Element) => {
    console.log(island)
    if (!(island instanceof HTMLElement)) return;

    try {
      const jsxString = island.innerHTML;
      const bindingsAttr = island.getAttribute('data-bindings');
      const bindings = bindingsAttr ? JSON.parse(bindingsAttr) : {};

      const root = createRoot(island);
      root.render(
        <IslandComponent
          jsxString={jsxString}
          bindings={bindings}
        />
      );
    } catch (error) {
      console.error('Error initializing React island:', error);
    }
  });
}

// Run initialization when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initializeIslands);
} else {
  initializeIslands();
}
