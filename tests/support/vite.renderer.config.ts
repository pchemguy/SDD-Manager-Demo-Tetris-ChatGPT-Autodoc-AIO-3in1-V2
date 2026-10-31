/** Independent renderer-test entry, excluded from runtime archives. */
import {defineConfig} from 'vite';
import {resolve} from 'node:path';
export default defineConfig({build:{outDir:'build/render-harness',emptyOutDir:true,rollupOptions:{input:resolve('tests/support/render.html')}}});
