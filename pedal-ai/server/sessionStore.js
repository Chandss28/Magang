const sessions = {};

export function getSession(id) {
  if (!sessions[id]) {
    sessions[id] = {
      weight: null,
      selectedSize: null
    };
  }
  return sessions[id];
}