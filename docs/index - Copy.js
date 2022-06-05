const express = require("express");
const axios = require("axios");
const cheerio = require("cheerio");
const cors = require("cors");
const app = express();
const PORT = process.env.PORT || 5000;
app.use(
  cors({
    //origin: 'avfreex24.com'
    
    origin: process.env.CORS_ORIGIN || "*",
  })
);
console.clear();
app.listen(PORT, () => console.log(`Serverr is listening on ${PORT}`));

const BASE_URL = "https://www.elitebabes.com/";
// routes

// home
app.get("/", async (req, res) => {
  try {
    let url = `${BASE_URL}`;

    let imageArr = [];
    const { data: html } = await axios(url);
    if (html) {
      let $ = cheerio.load(html);
      let images = $(".gallery-a li");
      images.each((i, el) => {
        if ($(el).find("img").attr("alt") && el.attribs.class !== "vid")
          imageArr.push({
            index: i,
            src:
              $(el).find("img").attr("srcset")?.split(" ")[0] ||
              $(el).find("img").attr("data-srcset")?.split(" ")[0] ||
              $(el).find("img").attr("src"),
            srcset: $(el).find("img").attr("srcset"),
            title: $(el).find("img").attr("alt"),
            link: $(el).find("a").attr("href")?.slice(27, -1),
          });
      });
    }
    res?.status(200).json({
      totalImages: imageArr?.length,
      images: imageArr,
    });
  } catch (error) {
    console.log(error.message);
    res.status(500).send("Error");
  }
});

// search
app.get("/search/:query", async (req, res) => {
  try {
    const { query } = req.params;
    const url = `${BASE_URL}/?s=${query}`;
    const { data } = await axios(url);
    const $ = cheerio.load(data);
    const models = [];
    const images = [];

    $(".gallery-a li").each((i, el) => {
      if (
        $(el).find("img").attr("alt") &&
        el.attribs.class !== "vid" &&
        !$(el).find("img").attr("src").endsWith(".svg")
      )
        if (
          $(el)
            .find("a")
            .attr("href")
            .startsWith("https://www.elitebabes.com/model")
        ) {
          models.push({
            src:
              $(el).find("img").attr("srcset")?.split(" ")[0] ||
              $(el).find("img").attr("data-srcset")?.split(" ")[0] ||
              $(el).find("img").attr("src"),
            name: $(el).find("img").attr("alt"),
            username: $(el).find("a").attr("href")?.slice(33, -1),
          });
        } else {
          images.push({
            src:
              $(el).find("img").attr("srcset")?.split(" ")[0] ||
              $(el).find("img").attr("data-srcset")?.split(" ")[0] ||
              $(el).find("img").attr("src"),
            title: $(el).find("img").attr("alt"),
            link: $(el).find("a").attr("href")?.slice(27, -1),
            new: $(el).find(".img span").first().text() ? true : false,
          });
        }
    });
    res?.status(200).json({
      query,
      totalModels: models?.length,
      models: models,
      totalImages: images?.length,
      images: images,
    });
  } catch (error) {
    console.log(error.message);
    res.status(500).send("Error");
  }
});

// models
app.get("/models", async (req, res) => {
  try {
    const { page } = req.query;
    let url = `${BASE_URL}/top-rated-babes/page/${page || 1}`;

    let imageArr = [];
    const { data: html } = await axios(url);
    if (html) {
      let $ = cheerio.load(html);
      let images = $(".gallery-a li");
      images.each((i, el) => {
        if ($(el).find("img").attr("alt") && el.attribs.class !== "vid")
          imageArr.push({
            src:
              $(el).find("img").attr("srcset")?.split(" ")[0] ||
              $(el).find("img").attr("data-srcset")?.split(" ")[0] ||
              $(el).find("img").attr("src"),
            name: $(el).find("img").attr("alt"),
            rank: $(el).find("span.strong").text(),
            username: $(el).find("a").attr("href")?.slice(33, -1),
          });
      });
    }
    res?.status(200).json({
      page: page || 1,
      totalModels: imageArr?.length,
      models: imageArr,
    });
  } catch (error) {
    console.log(error.message);
    res.status(500).send("Error");
  }
});

// studio
app.get("/studio", async (req, res) => {
  try {
    const { page, studio } = req.query;
    const url = `${BASE_URL}/${studio}/page/${page || 1}`;

    let imageArr = [];
    const { data: html } = await axios(url);

    let $ = cheerio.load(html);
    let images = $(".gallery-a li");
    images.each((i, el) => {
      if ($(el).find("img").attr("alt") && el.attribs.class !== "vid")
        imageArr.push({
          src:
            $(el).find("img").attr("srcset")?.split(" ")[0] ||
            $(el).find("img").attr("data-srcset")?.split(" ")[0] ||
            $(el).find("img").attr("src"),
          title: $(el).find("img").attr("alt"),
          link: $(el).find("a").attr("href")?.slice(27, -1),
        });
    });

    res?.status(200).json({
      page: page || 1,
      studio,
      name: $("h1.header-inline").text(),
      description: $(".text-center p").text(),
      totalModels: imageArr?.length,
      images: imageArr,
    });
  } catch (error) {
    console.log(error.message);
    res.status(500).send("Error");
  }
});

// single model
app.get("/model", async (req, res) => {
  try {
    const { username, page } = req.query;
    const url = `${BASE_URL}/model/${username}/mpage/${page || 1}`;

    let imageArr = [];
    const { data: html } = await axios(url);

    let $ = cheerio.load(html);
    let images = $(".gallery-a li");
    images.each((i, el) => {
      if ($(el).find("img").attr("alt") && el.attribs.class !== "vid")
        imageArr.push({
          src:
            $(el).find("img").attr("srcset")?.split(" ")[0] ||
            $(el).find("img").attr("data-srcset")?.split(" ")[0] ||
            $(el).find("img").attr("src"),
          title: $(el).find("img").attr("alt"),
          link: $(el).find("a").attr("href")?.slice(27, -1),
        });
    });

    res?.status(200).json({
      page: page || 1,
      username,
      poster: $(".module-model figure img")[0]?.attribs["srcset"]?.split(
        " "
      )[0],
      name: $(".fn").text()?.slice(0, " Favorites".length),
      desc1: $(".read-more-wrap").text(),
      desc2: $(".read-more").text(),
      totalImages: imageArr?.length,
      images: imageArr,
    });
  } catch (error) {
    console.log(error.message);
    res.status(500).send("Error");
  }
});

// single gallery
app.get("/gallery/:id", async (req, res) => {
  try {
    const { id } = req.params;
    const url = `${BASE_URL}/${id}`;

    let imageArr = [];
    const { data: html } = await axios(url);

    let $ = cheerio.load(html);
    let images = $(".gallery-a li");
    images.each((i, el) => {
      if ($(el).find("img").attr("alt") && el.attribs.class !== "vid")
        imageArr.push({
          src:
            $(el).find("img").attr("srcset")?.split(" ")[0] ||
            $(el).find("img").attr("data-srcset")?.split(" ")[0] ||
            $(el).find("img").attr("src"),
          title: $(el).find("img").attr("alt"),
          link: $(el).find("a").attr("href")?.slice(27, -1),
        });
    });

    const galleryImages = [];
    $(".list-gallery a").each((i, el) => {
      galleryImages.push({
        src: $(el).find("img").attr("src"),
        link: $(el).attr("href"),
      });
    });

    const studio = {};
    const tags = [];
    const models = [];
    $(".link-btn a").each((i, el) => {
      if ($(el).attr("href").startsWith("https://www.elitebabes.com/model"))
        models.push({
          username: $(el)?.attr("href")?.slice(33, -1),
          name: $(el)?.text(),
        });
      else if ($(el).attr("href").startsWith("https://www.elitebabes.com/tag/"))
        tags.push({
          tagName: $(el)?.text(),
          tag: $(el)?.attr("href")?.slice(31, -1),
        });
      else {
        studio.name = $(el)?.first().text();
        studio.link = $(el)?.attr("href")?.slice(27, -1);
      }
    });

    res?.status(200).json({
      id,
      title: $("title").text().slice(0, -" at Elite Babes".length),
      description: $(".header-inline").text(),
      tags: tags,
      models: models,
      studio: studio,
      images: galleryImages,
      related: imageArr,
    });
  } catch (error) {
    console.log(error.message);
    res.status(500).send("Error");
  }
});

// tag
app.get("/tag", async (req, res) => {
  try {
    const { tag, page } = req.query;
    const url = `${BASE_URL}/tag/${tag}/page/${page || 1}`;

    let imageArr = [];
    const { data: html } = await axios(url);

    let $ = cheerio.load(html);
    let images = $(".gallery-a li");
    images.each((i, el) => {
      if ($(el).find("img").attr("alt") && el.attribs.class !== "vid")
        imageArr.push({
          src:
            $(el).find("img").attr("srcset")?.split(" ")[0] ||
            $(el).find("img").attr("data-srcset")?.split(" ")[0] ||
            $(el).find("img").attr("src"),
          title: $(el).find("img").attr("alt"),
          link: $(el).find("a").attr("href")?.slice(27, -1),
        });
    });

    res?.status(200).json({
      page: page || 1,
      tag,
      totalImages: imageArr?.length,
      images: imageArr,
    });
  } catch (error) {
    console.log(error.message);
    res.status(500).send("Error");
  }
});

// newest
app.get("/latest", async (req, res) => {
  try {
    let url = `${BASE_URL}/latest-updates/`;

    let imageArr = [];
    const { data: html } = await axios(url);
    if (html) {
      let $ = cheerio.load(html);
      let images = $(".gallery-a li");
      images.each((i, el) => {
        if ($(el).find("img").attr("alt") && el.attribs.class !== "vid")
          imageArr.push({
            src:
              $(el).find("img").attr("srcset")?.split(" ")[0] ||
              $(el).find("img").attr("data-srcset")?.split(" ")[0] ||
              $(el).find("img").attr("src"),
            title: $(el).find("img").attr("alt"),
            date: $(el).find("span").first().text(),
            studio: {
              name: $(el).find(".displayblock").first().text(),
              link: $(el).find(".displayblock").attr("href").slice(27, -1),
            },
            link: $(el).find("a").attr("href")?.slice(27, -1),
          });
      });
    }
    res?.status(200).json({
      totalImages: imageArr?.length,
      images: imageArr,
    });
  } catch (error) {
    console.log(error.message);
    res.status(500).send("Error");
  }
});

// poplar
app.get("/popular", async (req, res) => {
  try {
    let url = `${BASE_URL}/trending/`;

    let imageArr = [];
    const { data: html } = await axios(url);
    if (html) {
      let $ = cheerio.load(html);
      let images = $(".gallery-a li");
      images.each((i, el) => {
        if ($(el).find("img").attr("alt") && el.attribs.class !== "vid")
          imageArr.push({
            src:
              $(el).find("img").attr("srcset")?.split(" ")[0] ||
              $(el).find("img").attr("data-srcset")?.split(" ")[0] ||
              $(el).find("img").attr("src"),
            title: $(el).find("img").attr("alt"),
            link: $(el).find("a").attr("href")?.slice(27, -1),
          });
      });
    }
    res?.status(200).json({
      totalImages: imageArr?.length,
      images: imageArr,
    });
  } catch (error) {
    console.log(error.message);
    res.status(500).send("Error");
  }
});


var AVapis = [{
  "id": 1,
  "name": "คลิปล่าสุด ส่งตรงจากจีน",
  "host": "https://sb8.app/rb8.png",
  "list_api": "http://f2dcj6.com/sapi/json?ac=list",
  "detail_api": "http://f2dcj6.com/sapi/json?ac=videolist", //&pg=&t=&wd=  &ids=106536,106535
},
{
  "id": 11,
  "name": "หนังAV ส่งตรงจากจีน",
  "host": "wu",
  "list_api": "http://zmcj88.com/sapi/json?ac=list",
  "detail_api": "http://zmcj88.com/sapi/json?ac=videolist", //&pg=&t=&wd=  &ids=106536,106535
},
{
  "id": 2,
  "name": "คลิปโซนเอเชีย",
  "host": "https://sao-lang-jian.com",
  "list_api": "http://llzxcj.com/inc/json.php?ac=list",
  "detail_api": "http://llzxcj.com/inc/json.php?ac=videolist",
},
{
  "id": 3,
  "name": "หนังAVเต็มเรื่อง",
  "host": "http://mygzycj.com",
  "list_api": "http://mygzycj.com/sapi.php?ac=jsonlist",
  "detail_api": "http://mygzycj.com/sapi.php?ac=jsonvideolist",
},

//รูปแบบ json ที่ส่งคืนโดย api ต่อไปนี้จะแตกต่างจากรูปแบบด้านบน ซึ่งแยกความแตกต่างด้วย id (id>100)
{
  "id": 100,
  "name": "💋AVวัยรุ่น",
  "host": "https://apilj.com/",
  "list_api": "https://apilj.com/api.php/provide/vod/at/json/?ac=list",
  "detail_api": "https://apilj.com/api.php/provide/vod/at/json/?ac=detail",
},
{
  "id": 101,
  "name": "🦆Cosplay Anime ",
  "host": "http://www.laoyazy5.com/",
  "list_api": "https://api.apilyzy.com/api.php/provide/vod/?ac=list",
  "detail_api": "https://api.apilyzy.com/api.php/provide/vod/?ac=detail",
},
{
  "id": 102,
  "name": "ANIME",
  "host": "http://help.apittzy.com/",
  "list_api": "https://apittzy.com/api.php/provide/vod/?ac=list",
  "detail_api": "https://apittzy.com/api.php/provide/vod/?ac=detail",
  "art": "https://apittzy.com/api.php/provide/art/?ac=", //ac=list  ac=detail
},
{
  "id": 103,
  "name": "INTERเย็ดกัน",
  "host": "https://api.xiuseapi.com/",
  "list_api": "https://api.xiuseapi.com/api.php/provide/vod/?ac=list",
  "detail_api": "https://api.xiuseapi.com/api.php/provide/vod/?ac=detail",
  "art": "https://api.xiuseapi.com/api.php/provide/art/?ac=", //ac=list  ac=detail
},
{
  "id": 104,
  "name": "🐠แหล่งตกเบ็ด",
  "host": "https://help.leyuzy.pro/",
  "list_api": "https://www.leyuzyapi.com/inc/apijson_vod.php?ac=list",
  "detail_api": "https://www.leyuzyapi.com/inc/apijson_vod.php?ac=detail",
  "jx": "https://player.leyuzy.net/?url=",
},
{
  "id": 105,
  "name": "🧦ถุงน่อง",
  "host": "https://siwazyw.tv/index.php/label/help.html",
  "list_api": "https://siwazyw.tv/api.php/provide/vod/?ac=list",
  "detail_api": "https://siwazyw.tv/api.php/provide/vod/?ac=detail",
  "art": "https://siwazyw.tv/api.php/provide/art/?ac=", //ac=list  ac=detail
  "jx": "http://jx.siwapay.com/m3u8.php?url=",
},
{
  "id": 106,
  "name": "INTERSHOW",
  "host": "https://www.kudouzy.com/index.php/label/help.html",
  "list_api": "http://api.kdapi.info/api.php/provide/vod/?ac=list",
  "detail_api": "http://api.kdapi.info/api.php/provide/vod/?ac=detail",
  "art": "http://api.kdapi.info/api.php/provide/art/?ac=detail", //ac=list  ac=detail
  "jx": "https://jx.kubohk.com/jx/?url=",
},
{
  "id": 107,
  "name": "🥑AV",
  "host": "https://mgm3u8-player.com/",
  "list_api": "https://mgzyz1.com/api.php/provide/vod/?ac=list",
  "detail_api": "https://mgzyz1.com/api.php/provide/vod/?ac=detail",
  "jx": "https://mgm3u8-player.com/player/DPm3u8.php?url=",
},
{
  "id": 108,
  "name": "🍑ทรัพยากรพีช",
  "host": "http://51smt4.xyz/",
  "list_api": "http://51smt4.xyz/api.php/provide/vod/?ac=list",
  "detail_api": "http://51smt4.xyz/api.php/provide/vod/?ac=detail",
},
{
  "id": 109,
  "name": "🌶อินเตอร์แซ่บๆ",
  "host": "https://apihjzy.com",
  "list_api": "https://apihjzy.com/api.php/provide/vod/at/json/?ac=detail",
  "detail_api": "https://apihjzy.com/api.php/provide/vod/at/json/?ac=detail",
},
{
  "id": 110,
  "name": "😄JAV",
  "host": "https://lbapi9.com",
  "list_api": "https://lbapi9.com/api.php/provide/vod/at/json/?ac=list",
  "detail_api": "https://lbapi9.com/api.php/provide/vod/at/json/?ac=detail",
},
// {
//   "id": 111,
//   "name": "😄ทรัพยากรจำนวน",
//   "host": "https://fhapi9.com",
//   "list_api": "http://fhapi9.com/api.php/provide/vod/at/json/?ac=list",
//   "detail_api": "http://fhapi9.com/api.php/provide/vod/at/json/?ac=detail",
// },
{
  "id": 112,
  "name": "🦈ทีมฉลาม",
  "host": "www.shayuapi.com",
  "list_api": "https://www.shayuapi.com/api.php/provide/vod/at/json/?ac=list",
  "detail_api": "https://www.shayuapi.com/api.php/provide/vod/at/json/?ac=detail",
},
{
  "id": 113,
  "name": "🥑AV",
  "host": "www.mgav1.cc",
  "list_api": "https://www.mgav1.cc/api.php/provide/vod/at/json/?ac=detail",
  "detail_api": "https://www.mgav1.cc/api.php/provide/vod/at/json/?ac=detail",
}
]


// // newest
// app.get("/av-movie-new", async (req, res) => {
  
//   const {host}  = req.query;
//   var hostapi = AVapis[host || 1].detail_api
//   try {
//     let url = `${hostapi}`;
//     console.log(url);
//     let imageArr = [];
//     const { data: html } = await axios(url);
//     if (html) {
//       let item_av = html.data || html.list
//       for(ix=0; ix < item_av.length; ix++){ 

//         let av_vidpath = item_av[ix].vpath || item_av[ix].vod_play_url;
//         if (av_vidpath.indexOf('$') != -1)
//         av_vidpath = av_vidpath.split('$')[1].split('#')[0];
//         imageArr.push({
//           avfreex24_file: av_vidpath,
//           //avfreex24_title_th: av_vod_title_tr ,
//           title: item_av[ix].vod_title || item_av[ix].vod_name,
//           avfreex24_vod_id: item_av[ix].vod_id,
//           avfreex24_vod_cid: item_av[ix].vod_cid,
//           avfreex24_vod_addtime: item_av[ix].vod_addtime || item_av[ix].vod_time,
//           //avfreex24_category_th: category_thtr,
//           avfreex24_category_def: item_av[ix].category || item_av[ix].vod_class,
//           src: item_av[ix].vod_pic,
//           avfreex24_vod_language: item_av[ix].vod_language,
//           avfreex24_vod_area: item_av[ix].vod_area,
//           avfreex24_vod_year: item_av[ix].vod_year,
//           avfreex24_state: item_av[ix].state,
//           avfreex24_vod_actor: item_av[ix].vod_actor,
//           avfreex24_vod_director: item_av[ix].vod_director,
//           avfreex24_playfrom: item_av[ix].playfrom,
//           //vod_content_th: av_vod_content_th,
//           avfreex24_vod_content: item_av[ix].vod_content
//         });
//       }
//     }
//     res?.status(200).json({
//       totalImages: imageArr?.length,
//       images: imageArr,
//     });
//   } catch (error) {
//     console.log(error.message);
//     res.status(500).send("Error");
//   }
// });


// // single AvPlayer
// app.get("/play-avfreex24/:id", async (req, res) => {
//   try {
//     const { id } = req.params;
//     const url = `${BASE_URL}/${id}`;

//     let imageArr = [];
//     const { data: html } = await axios(url);

//     let $ = cheerio.load(html);
//     let images = $(".gallery-a li");
//     images.each((i, el) => {
//       if ($(el).find("img").attr("alt") && el.attribs.class !== "vid")
//         imageArr.push({
//           src:
//             $(el).find("img").attr("srcset")?.split(" ")[0] ||
//             $(el).find("img").attr("data-srcset")?.split(" ")[0] ||
//             $(el).find("img").attr("src"),
//           title: $(el).find("img").attr("alt"),
//           link: $(el).find("a").attr("href")?.slice(27, -1),
//         });
//     });

//     const galleryImages = [];
//     $(".list-gallery a").each((i, el) => {
//       galleryImages.push({
//         src: $(el).find("img").attr("src"),
//         link: $(el).attr("href"),
//       });
//     });

//     const studio = {};
//     const tags = [];
//     const models = [];
//     $(".link-btn a").each((i, el) => {
//       if ($(el).attr("href").startsWith("https://www.elitebabes.com/model"))
//         models.push({
//           username: $(el)?.attr("href")?.slice(33, -1),
//           name: $(el)?.text(),
//         });
//       else if ($(el).attr("href").startsWith("https://www.elitebabes.com/tag/"))
//         tags.push({
//           tagName: $(el)?.text(),
//           tag: $(el)?.attr("href")?.slice(31, -1),
//         });
//       else {
//         studio.name = $(el)?.first().text();
//         studio.link = $(el)?.attr("href")?.slice(27, -1);
//       }
//     });

//     res?.status(200).json({
//       id,
//       title: $("title").text().slice(0, -" at Elite Babes".length),
//       description: $(".header-inline").text(),
//       tags: tags,
//       models: models,
//       studio: studio,
//       images: galleryImages,
//       related: imageArr,
//     });
//   } catch (error) {
//     console.log(error.message);
//     res.status(500).send("Error");
//   }
// });


// avsb8
//http://localhost:5000/avsb?host=0&page=3

app.get("/avsb", async (req, res) => {
  var ip = req.headers['x-forwarded-for'] || req.socket.remoteAddress;
  var origin = req.get('origin');
  
  const {host}  = req.query;
  var hostapi = AVapis[host || 0].detail_api
  try {
    const { page } = req.query;
    var BASE_URL_AVsb8 = `${hostapi}&pg=${page || 1}`
    let url = `${BASE_URL_AVsb8}`;
    let vidAVArr = [];
    const { data: html } = await axios(url);
    //console.log(html.pagecount)
    if (html) {
      let item_av = html.data || html.list
      for(ix=0; ix < item_av.length; ix++){ 
        let av_vidpath = item_av[ix].vpath || item_av[ix].vod_play_url;
        if (av_vidpath.indexOf('$') != -1)
        av_vidpath = av_vidpath.split('$')[1].split('#')[0];
        vidAVArr.push({
          avfreex24_file: av_vidpath,
          //avfreex24_title_th: av_vod_title_tr ,
          avfreex24_title: item_av[ix].vod_title || item_av[ix].vod_name,
          avfreex24_vod_id: item_av[ix].vod_id,
          avfreex24_vod_cid: item_av[ix].vod_cid,
          avfreex24_vod_addtime: item_av[ix].vod_addtime || item_av[ix].vod_time,
          //avfreex24_category_th: category_thtr,
          avfreex24_category_def: item_av[ix].category || item_av[ix].vod_class,
          avfreex24_src: item_av[ix].vod_pic,
          avfreex24_vod_language: item_av[ix].vod_language,
          avfreex24_vod_area: item_av[ix].vod_area,
          avfreex24_vod_year: item_av[ix].vod_year,
          avfreex24_state: item_av[ix].state,
          avfreex24_vod_actor: item_av[ix].vod_actor,
          avfreex24_vod_director: item_av[ix].vod_director,
          avfreex24_playfrom: item_av[ix].playfrom,
          //vod_content_th: av_vod_content_th,
          avfreex24_vod_content: item_av[ix].vod_content
        });
      }
    }
    res?.status(200).json({
      page: page || 1,
      AV_pagecount: html.pagecount,
      AV_total: html.total,
      AV_ip: ip,
      AV_origin: origin,
      AVFORPAGE_AV: vidAVArr?.length,
      AV_ITEMS: vidAVArr,
    });
  } catch (error) {
    console.log(error.message);
    res.status(500).send("Error");
  }
});

app.get("/jwlist", async (req, res) => {
  var ip = req.headers['x-forwarded-for'] || req.socket.remoteAddress;
  var origin = req.get('origin');
  //if(origin != "http://localhost:1313" || origin != "https://avfreex24.com/fw.html" ){
  //      return;
  //}
  const {host}  = req.query;
  var hostapi = AVapis[host || 0].detail_api
  try {
    const { page } = req.query;
    var BASE_URL_AVsb8 = `${hostapi}&pg=${page || 1}`
    let url = `${BASE_URL_AVsb8}`;
    let vidAVArr = [];
    const { data: html } = await axios(url);
    //console.log(html.data)
    if (html) {
      let item_av = html.data || html.list
      for(ix=0; ix < item_av.length; ix++){ 
        let av_vidpath = item_av[ix].vpath || item_av[ix].vod_play_url;
        if (av_vidpath.indexOf('$') != -1)
        av_vidpath = av_vidpath.split('$')[1].split('#')[0];
        vidAVArr.push({
          file: av_vidpath,
          title: item_av[ix].vod_title || item_av[ix].vod_name,
          mediaid: item_av[ix].vod_id,
          image: item_av[ix].vod_pic
        });
      }
    }
    res?.status(200).json({
      page: page || 1,
      AV_pagecount: html.pagecount,
      AV_total: html.total,
      AV_ip: ip,
      AV_origin: origin,
      AVFORPAGE_AV: vidAVArr?.length,
      AV_FW_ITEMS: vidAVArr,
    });
  } catch (error) {
    console.log(error.message);
    res.status(500).send("Error");
  }
});
