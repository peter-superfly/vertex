/*global localStorage*/
export const getLS = (key) => {
  let isSSR = typeof window === "undefined";

  if (isSSR) return null;

  const value = localStorage.getItem(key);
  try {
    return JSON.parse(value);
  } catch (e) {
    console.error(e);
    return null;
  }
};

export const setLS = (key, value) => {
  localStorage.setItem(key, JSON.stringify(value));
};

export const clearLS = () => localStorage.clear();
