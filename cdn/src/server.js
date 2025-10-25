import 'dotenv/config';
import { buildApp } from './app.js';

const PORT = Number(process.env.PORT || 4001);

const app = buildApp();
app.listen(PORT, () => {
  // eslint-disable-next-line no-console
  console.log(`File service running on http://localhost:${PORT}`);
});
