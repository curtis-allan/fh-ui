const [count, setCount] = signal(0); // state value set to 0

setInterval(() => setCount((prev) => prev + 1), 1000);

effect(() => {
  console.log("Count has changed!", count());
});
