import { useState } from "react";
import API from "./api";
import "./App.css";

function App() {

  const [studentName, setStudentName] = useState("");
  const [courseName, setCourseName] = useState("");
  const [trainerName, setTrainerName] = useState("");
  const [review, setReview] = useState("");

  const [result, setResult] = useState("");

  const [reviews, setReviews] = useState([]);

  const [showReviews, setShowReviews] = useState(false);

  // Fetch Reviews
  const fetchReviews = async () => {

    try {

      const response = await API.get("/reviews");

      setReviews(response.data);

    } catch (error) {

      console.log(error);

      alert("Unable to fetch reviews");

    }

  };

  // Submit Review
  const submitReview = async () => {

    if (
      !studentName ||
      !courseName ||
      !trainerName ||
      !review
    ) {

      alert("Please fill all fields");

      return;

    }

    try {

      const response = await API.post("/predict", {

        student_name: studentName,

        course_name: courseName,

        trainer_name: trainerName,

        review: review

      });

      setResult(response.data["Predicted Sentiment"]);

      alert("Review Submitted Successfully!");

      setStudentName("");

      setCourseName("");

      setTrainerName("");

      setReview("");

    }

    catch (error) {

      console.log(error);

      alert("Backend Connection Error");

    }

  };

  return (

    <div className="container">

      <div className="card">

        <h1>Sentiment Analysis of Student Reviews</h1>

        <p className="subtitle">

          Analyze student feedback using Machine Learning

        </p>

        <input
          type="text"
          placeholder="Student Name"
          value={studentName}
          onChange={(e)=>setStudentName(e.target.value)}
        />

        <input
          type="text"
          placeholder="Course Name"
          value={courseName}
          onChange={(e)=>setCourseName(e.target.value)}
        />

        <input
          type="text"
          placeholder="Trainer Name"
          value={trainerName}
          onChange={(e)=>setTrainerName(e.target.value)}
        />

        <textarea
          rows="5"
          placeholder="Write your review..."
          value={review}
          onChange={(e)=>setReview(e.target.value)}
        />

        <button onClick={submitReview}>

          Submit Review

        </button>

        {

          result &&

          <div className="result-box">

            <h2>Prediction Result</h2>

            <h3>{result}</h3>

          </div>

        }

        <button

          style={{marginTop:"20px"}}

          onClick={async()=>{

            if(!showReviews){

              await fetchReviews();

            }

            setShowReviews(!showReviews);

          }}

        >

          {

            showReviews

            ?

            "Hide Reviews"

            :

            "View All Reviews"

          }

        </button>

        {

          showReviews &&

          <>

            <h2 style={{marginTop:"30px"}}>

              All Student Reviews

            </h2>

            <table>

              <thead>

                <tr>

                  <th>Student</th>

                  <th>Course</th>

                  <th>Trainer</th>

                  <th>Review</th>

                  <th>Sentiment</th>

                  <th>Date</th>

                </tr>

              </thead>

              <tbody>

                {

                  reviews.length > 0 ?

                  (

                    reviews.map((item,index)=>(

                      <tr key={index}>

                        <td>{item.student_name}</td>

                        <td>{item.course_name}</td>

                        <td>{item.trainer_name}</td>

                        <td>{item.review}</td>

                        <td>{item.sentiment}</td>

                        <td>{item.review_date}</td>

                      </tr>

                    ))

                  )

                  :

                  (

                    <tr>

                      <td colSpan="6">

                        No Reviews Found

                      </td>

                    </tr>

                  )

                }

              </tbody>

            </table>

          </>

        }

      </div>

    </div>

  );

}

export default App;