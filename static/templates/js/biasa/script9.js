const Countdown = (date) => {
  console.log(date);
  const ct = new Date(date).getTime();

  const x = setInterval(() => {
    let now = new Date().getTime();

    let distance = ct - now;

    let days = Math.floor(distance / (1000 * 60 * 60 * 24));
    let hours = Math.floor(
      (distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)
    );
    let minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    let seconds = Math.floor((distance % (1000 * 60)) / 1000);

    if (distance <= 0) {
      clearInterval(x);
    } else {
      $(".days .angka").text(days);
      $(".hours .angka").text(hours);
      $(".minutes .angka").text(minutes);
      $(".seconds .angka").text(seconds);
    }
  }, 1000);
};
