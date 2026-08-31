import { webcore } from 'webcoreui/integration';
import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://alimie.github.io',
  base: '/notabelajar',
  integrations: [webcore()],
});