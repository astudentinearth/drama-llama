import 'dotenv/config';

export function requireUser(req, res, next) {
  const uid = req.header('x-user-id');
  if (!uid) return res.status(401).json({ error: 'Unauthenticated' });
  req.user = { id: uid };
  next();
}
