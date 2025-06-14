export const sleep = (ms: number) =>
  new Promise((resolve) => {
    setTimeout(() => {
      console.log("Sleeping for 3 seconds");
      resolve(true);
    }, ms);
  });
