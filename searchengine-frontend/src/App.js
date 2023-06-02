import React, { useState } from "react";
import CircularProgress from "@mui/material/CircularProgress";
import Box from "@mui/material/Box";

function App() {
  const [searchInput, setSearchInput] = useState("");
  const [searched, setSearched] = useState(false);
  const [websiteList, setWebsitesList] = useState([]);
  const [loading, setLoading] = useState(null);
  const [contentType, setContentType] = useState("text");

  const onOptionChange = (e) => {
    setContentType(e.target.value);
  };
  function clickSearchButton() {
    setSearched(true);
    setLoading(true);
    console.log(searchInput);
    const requestOptions = {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin":
          "https://8afa-210-6-189-186.ngrok-free.app",
        "Access-Control-Allow-Credentials": "true",
      },
      body: JSON.stringify({ type: contentType, query: searchInput }),
    };
    fetch(
      "https://8afa-210-6-189-186.ngrok-free.app/api/search",
      requestOptions
    )
      .then((response) => response.json())
      .then((data) => {
        setWebsitesList(data.websites);
        console.log(data);
        setLoading(false);
      });
  }
  function handleInputChange(e) {
    setSearchInput(e.target.value);
  }

  return (
    <h1 className=" bg-school w-full h-screen p-4">
      <div className=" container max-w-xl  mx-auto">
        <h1
          className={
            " font-Lora text-center font-bold text-5xl text-cyan-400 " +
            (searched ? "pt-12" : "pt-40")
          }
        >
          Smart O2O System
        </h1>
        <div className=" py-10">
          <div className="flex border border-purple-200 rounded">
            <input
              type="text"
              className="block w-full px-4 py-2 text-purple-700 bg-white border rounded-md focus:border-purple-400 focus:ring-purple-300 focus:outline-none focus:ring focus:ring-opacity-40"
              placeholder="Search..."
              value={searchInput}
              onChange={handleInputChange}
            />
            <button
              className="px-4 text-white bg-purple-600 border-l rounded "
              onClick={clickSearchButton}
            >
              Search
            </button>
          </div>
          <div className="bg-cyan-100 rounded-lg p-3  flex space-x-4 ">
            <input
              type="radio"
              name="contentType"
              value="text"
              id="text"
              checked={contentType === "text"}
              onChange={onOptionChange}
            />
            <label
              htmlFor="text"
              className=" text-base text-cyan-800 font-Montserrat font-bold"
            >
              Text
            </label>

            <input
              type="radio"
              name="contentType"
              value="image"
              id="image"
              checked={contentType === "image"}
              onChange={onOptionChange}
            />
            <label
              htmlFor="image"
              className=" text-base text-cyan-800 font-Montserrat font-bold"
            >
              Image
            </label>

            <input
              type="radio"
              name="contentType"
              value="video"
              id="video"
              checked={contentType === "video"}
              onChange={onOptionChange}
            />
            <label
              htmlFor="video"
              className=" text-base text-cyan-800 font-Montserrat font-bold"
            >
              Video
            </label>
          </div>
        </div>
        {loading && (
          <Box
            sx={{
              weight: 140,
              height: 140,
              display: "flex",
              justifyContent: "center",
            }}
          >
            <CircularProgress size="30vh" />
          </Box>
        )}
        {searchInput.length > 0 && !loading && (
          <div>
            {websiteList.map((item, index) => (
              <div key={index} className=" bg-slate-100 rounded-lg p-3 mb-4">
                <a
                  href={item.url}
                  className=" text-2xl font-Montserrat text-black-500 font-semibold "
                >
                  {item.title}
                </a>
                <div className=" text-base text-orange-500 font-Lora ">
                  {item.content}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </h1>
  );
}

export default App;
