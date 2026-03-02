let stats = {
  totalChats: 0,
  sizeRequests: {
    XXS: 0,
    XS: 0,
    S: 0
  }
};

export function logChat() {
  stats.totalChats++;
}

export function logSize(size) {
  if (stats.sizeRequests[size] !== undefined) {
    stats.sizeRequests[size]++;
  }
}

export function getStats() {
  return stats;
}