/** Browser-only entropy port; no game rules or stored session history. */
export function seed():number{return crypto.getRandomValues(new Uint32Array(1))[0];}
