import express from 'express';
import cors from 'cors';

const app = express();
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.get('/price/:number', (req, res) => {
  const price = parseInt(req.params.number) * 0.014174;
  res.send(price.toString());
});

app.listen(5001, () => {
  console.log('Price calculator listening on port 5001');
});

export default app;
