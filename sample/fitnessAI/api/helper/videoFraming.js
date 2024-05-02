const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');  // For running shell commands, like ffmpeg

class VideoFraming {
    constructor(filePath, targetFolder) {
        this.filePath = filePath;
        this.fileName = path.basename(filePath).replace('.mp4', "");
        this.targetFolder = targetFolder;

        this.outputFolder = this.createTempStorage();
        this.frameList = [];

        this.updateNaming();
        this.extractFrames();
    }

    updateNaming() {
        if (this.fileName.includes('.')) {
            this.fileName = this.fileName.replace(/\./g, '_');
        }
    }

    createTempStorage() {
        const outputDir = `${path.join(this.targetFolder, `js_${this.fileName}`)}`;
        if (fs.existsSync(outputDir)) {
            fs.rmdirSync(outputDir, { recursive: true });
        }
        fs.mkdirSync(outputDir, { recursive: true });
        return outputDir;
    }

    extractFrames() {
        const fps = 1; // Frames per second
        const totalSeconds = parseInt(execSync(`ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "${this.filePath}"`, { encoding: 'utf8' }).trim());
        
        for (let second = 0; second < totalSeconds; second += 1) {
            const minutes = Math.floor(second / 60);
            const seconds = second % 60;
            const outputFilename = `${this.outputFolder}/${this.fileName}_frame${minutes.toString().padStart(2, '0')}-${seconds.toString().padStart(2, '0')}.png`;
            const command = `ffmpeg -ss ${second} -i "${this.filePath}" -frames:v 1 -q:v 1 -f image2 "${outputFilename}"`;
            try {
                execSync(command);
                this.frameList.push(outputFilename);  // Keep track of output files
            } catch (error) {
                console.error("Error extracting frame at second " + second + ": ", error);
            }
        }
        console.log("Completed video frame extraction!");
    }

    getFrameList() {
        const files = fs.readdirSync(this.outputFolder);
        files.forEach(file => {
            this.frameList.push(new File(path.join(this.outputFolder, file)));
        });
    }
}

class File {
    constructor(filePath) {
        this.filePath = filePath;
        this.display_name = path.basename(filePath);
        this.timestamp = this.getTimestamp(this.display_name);
    }

    getTimestamp(filename) {
        const parts = filename.split('_frame');
        if (parts.length !== 2) {
            return null;  // Indicates the filename might be incorrectly formatted
        }
        const timePart = parts[1].split('.')[0];
        const [minutes, seconds] = timePart.split('-');
        return `${minutes}:${seconds}`;
    }
}

// Usage example
const videoPath = path.join(__dirname, '..', '..', 'content', 'videos', '2024.04.11_GYM_ADAM.mp4');
const outputPath = path.join(__dirname, '..', '..', 'content', 'parsed_outputs');
const videoProcessor = new VideoFraming(
    filePath=`${videoPath}`,
    targetFolder=`${outputPath}`
);
const files = videoProcessor.getFrameList()
console.log(videoProcessor.frameList)

/*
Run the file once to see the output in the frameList object of the
class.

Note: if any editing to the function need to be made in the class
videoFraming, any "ffmpeg" related command should be cautious about
file paths. ie. any path.join object should be wrapped with ""

FFMPEG also needs to be added to PATH to run locally -- this is for
windows.

Package: https://ffmpeg.org/download.html
*/
