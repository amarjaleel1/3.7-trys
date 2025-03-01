/**
 * Additional lessons for the AI Learning Platform
 * Import these into lessons.js when you want to add them
 */

const additionalLessons = [
    {
        id: 'unsupervised',
        title: 'Unsupervised Learning: Clustering',
        content: `
            <h3>Unsupervised Learning: Clustering</h3>
            <p>Unsupervised learning allows AI to find patterns in data without explicit labels.</p>
            <p>K-means clustering is one of the most common clustering algorithms, grouping data points based on similarity.</p>
            <h4>Task:</h4>
            <p>Implement a function that assigns data points to the nearest of K centroids.</p>
        `,
        task: 'Create a function called assignToClusters(dataPoints, centroids) that returns an array of cluster assignments',
        hint: 'Calculate the Euclidean distance between each point and each centroid, then assign to the closest one',
        requiredCoins: 40,
        starterCode: `// K-Means Clustering - Assign Points to Clusters
function assignToClusters(dataPoints, centroids) {
  // dataPoints is an array of {x, y} coordinates
  // centroids is an array of {x, y} coordinates representing K cluster centers
  
  // Return an array where each element is the index of the closest centroid
  // for the corresponding data point
  
  // Your code here
  
}

// Helper function to calculate Euclidean distance
function distance(point1, point2) {
  return Math.sqrt(Math.pow(point1.x - point2.x, 2) + Math.pow(point1.y - point2.y, 2));
}
`,
        checkCode: function(code) {
            return code.includes('function assignToClusters') && 
                   code.includes('distance') && 
                   code.includes('return');
        }
    },
    {
        id: 'genetic',
        title: 'Genetic Algorithms',
        content: `
            <h3>Genetic Algorithms</h3>
            <p>Genetic algorithms are optimization techniques inspired by natural selection.</p>
            <p>They evolve solutions through operations like selection, crossover, and mutation.</p>
            <h4>Task:</h4>
            <p>Implement a function that performs crossover between two parent chromosomes (represented as binary strings).</p>
        `,
        task: 'Create a function called crossover(parent1, parent2) that performs single-point crossover',
        hint: 'Choose a random crossover point, then combine the first part of parent1 with the second part of parent2',
        requiredCoins: 50,
        starterCode: `// Genetic Algorithm - Crossover Operation
function crossover(parent1, parent2) {
  // parent1 and parent2 are binary strings of the same length
  // Example: parent1 = "10101", parent2 = "11010"
  
  // Return a new offspring created by combining parts of both parents
  // using single-point crossover
  
  // Your code here
  
}
`,
        checkCode: function(code) {
            return code.includes('function crossover') && 
                   code.includes('Math.random') && 
                   (code.includes('substring') || code.includes('slice'));
        }
    },
    {
        id: 'nlp',
        title: 'Natural Language Processing',
        content: `
            <h3>Natural Language Processing (NLP)</h3>
            <p>NLP enables computers to understand, interpret, and generate human language.</p>
            <p>Tokenization is a fundamental step in many NLP pipelines.</p>
            <h4>Task:</h4>
            <p>Implement a function that tokenizes a sentence into words and removes common stop words.</p>
        `,
        task: 'Create a function called tokenize(text, stopWords) that splits text into tokens and removes stop words',
        hint: 'Split the text by spaces, then filter out any tokens that exist in the stopWords array',
        requiredCoins: 60,
        starterCode: `// Natural Language Processing - Tokenization
function tokenize(text, stopWords) {
  // text is a string containing a sentence
  // stopWords is an array of common words to remove (e.g., ["the", "a", "and"])
  
  // Return an array of tokens (words) with stop words removed
  
  // Your code here
  
}

// Example usage:
// const text = "The quick brown fox jumps over the lazy dog";
// const stopWords = ["the", "over", "the"];
// tokenize(text, stopWords) should return ["quick", "brown", "fox", "jumps", "lazy", "dog"]
`,
        checkCode: function(code) {
            return code.includes('function tokenize') && 
                   (code.includes('split') || code.includes('match')) && 
                   code.includes('filter');
        }
    },
    {
        id: 'computer-vision',
        title: 'Computer Vision Basics',
        content: `
            <h3>Computer Vision Basics</h3>
            <p>Computer Vision enables machines to interpret and make decisions based on visual data.</p>
            <p>Simple image processing operations form the foundation of many computer vision algorithms.</p>
            <h4>Task:</h4>
            <p>Implement a function that performs a simple image threshold operation.</p>
        `,
        task: 'Create a function called thresholdImage(imageData, threshold) that converts pixel values to either 0 or 255 based on a threshold',
        hint: 'Loop through the imageData array and for each pixel value, set it to 0 if it\'s below the threshold or 255 if it\'s above',
        requiredCoins: 70,
        starterCode: `// Computer Vision - Image Thresholding
function thresholdImage(imageData, threshold) {
  // imageData is a flat array of pixel values (0-255)
  // threshold is a value between 0-255
  
  // Return a new array where each pixel is either 0 (if below threshold)
  // or 255 (if above or equal to threshold)
  
  // Your code here
  
}

// Example usage:
// const image = [100, 150, 200, 50, 180, 90, 255, 30];
// thresholdImage(image, 100) should return [0, 255, 255, 0, 255, 0, 255, 0]
`,
        checkCode: function(code) {
            return code.includes('function thresholdImage') && 
                   code.includes('threshold') && 
                   (code.includes('for') || code.includes('map') || code.includes('forEach'));
        }
    }
];

// Function to add additional lessons to the main lessons array
function addAdditionalLessons(mainLessons) {
    additionalLessons.forEach(lesson => {
        mainLessons.push(lesson);
    });
    return mainLessons;
}

// Export for use in lessons.js
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { additionalLessons, addAdditionalLessons };
}