import 'vite/modulepreload-polyfill'
import * as Components from '@/components'
import './index.css'
import { createRoot } from 'react-dom/client';

function renderComps() {
  document.querySelectorAll('.react-component')
    .forEach(el => {
      const props = JSON.parse(el.getAttribute('data-attrs')!);

      console.log(props);

      const children = el.innerHTML || '';
      //@ts-expect-error import
      const Component = Components[el.dataset.tag]!

      const comp = (<Component {...props} dangerouslySetInnerHTML={{ __html: children }} />);

      const container = document.createElement('div')

      //@ts-expect-error import
      htmx.onLoad(() => {
        el.replaceWith(container)
        const root = createRoot(container);
        root.render(comp)
      });

      //  .render(<Component {...props}>{children}</Component>)
    });
}

renderComps()

document.body.addEventListener("htmx:afterSwap", renderComps)
