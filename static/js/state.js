// Minimal component-based state store
const Store = (function(){
  let state = {};
  const subs = {};
  return {
    get(k){ return state[k] },
    set(k,v){ state[k]=v; (subs[k]||[]).forEach(fn=>fn(v)); },
    subscribe(k,fn){ subs[k]=subs[k]||[]; subs[k].push(fn) }
  }
})();
window.Store = Store;
