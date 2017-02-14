<?php

require_once "src/QueryBuilder.php";
require_once "src/UploadProcessor.php";
require_once "src/DataProcessor.php";
require_once "src/MuBench/Detector.php";
require_once "src/MuBench/Misuse.php";
require_once "DatabaseTestCase.php";

use MuBench\Detector;
use MuBench\Misuse;

class StoreFindingsTest extends DatabaseTestCase
{

    function test_store_ex1()
    {
        $queryBuilder = new QueryBuilder($this->pdo, $this->logger);
        $upload_processor = new UploadProcessor($this->db, $queryBuilder, $this->logger);
        $data_processor = new DataProcessor($this->db, $this->logger);

        $data = json_decode($this->finding_json);
        $upload_processor->processData("ex1", $data, $data->{"potential_hits"});
        $detector = $data_processor->getDetector("-d-");
        $runs = $data_processor->getRuns($detector, "ex1");

        $expected_run = [
            "exp" => "ex1",
            "project" => "-p-",
            "version" => "-v-",
            "result" => "success",
            "runtime" => "42.1",
            "number_of_findings" => "23",
            "detector" => "detector_1",
            "misuses" => []
        ];

        self::assertEquals([$expected_run], $runs);
    }

    function test_store_ex2()
    {
        $queryBuilder = new QueryBuilder($this->pdo, $this->logger);
        $upload_processor = new UploadProcessor($this->db, $queryBuilder, $this->logger);
        $data_processor = new DataProcessor($this->db, $this->logger);

        $data = json_decode($this->finding_json);
        $upload_processor->processData("ex2", $data, $data->{"potential_hits"});
        $detector = $data_processor->getDetector("-d-");
        $runs = $data_processor->getRuns($detector, "ex2");

        $expected_run = [
            "exp" => "ex2",
            "project" => "-p-",
            "version" => "-v-",
            "result" => "success",
            "runtime" => "42.1",
            "number_of_findings" => "23",
            "detector" => "detector_1",
            "misuses" => [
                new Misuse(
                    ["misuse" => "0", "snippets" => [0 => ["line" => "5", "snippet" => "-code-"]]],
                    [0 => [
                        "exp" => "ex2",
                        "project" => "-p-",
                        "version" => "-v-",
                        "misuse" => "0",
                        "rank" => "0",
                        "custom1" => "-val1-",
                        "custom2" => "-val2-"
                    ]
                    ],
                    []
                )
            ]
        ];
        self::assertEquals([$expected_run], $runs);
    }

    function test_store_ex3()
    {
        $queryBuilder = new QueryBuilder($this->pdo, $this->logger);
        $upload_processor = new UploadProcessor($this->db, $queryBuilder, $this->logger);
        $data_processor = new DataProcessor($this->db, $this->logger);

        $data = json_decode($this->finding_json);
        $upload_processor->processData("ex3", $data, $data->{"potential_hits"});
        $detector = $data_processor->getDetector("-d-");
        $runs = $data_processor->getRuns($detector, "ex3");

        $expected_run = [
            "exp" => "ex3",
            "project" => "-p-",
            "version" => "-v-",
            "result" => "success",
            "runtime" => "42.1",
            "number_of_findings" => "23",
            "detector" => "detector_1",
            "misuses" => []
        ];

        self::assertEquals([$expected_run], $runs);
    }

    function test_get_misuse_ex1(){
        $queryBuilder = new QueryBuilder($this->pdo, $this->logger);
        $upload_processor = new UploadProcessor($this->db, $queryBuilder, $this->logger);
        $data_processor = new DataProcessor($this->db, $this->logger);

        $data = json_decode($this->finding_json);
        $metadata = json_decode($this->metadata_json);
        $upload_processor->processData("ex1", $data, $data->{"potential_hits"});
        $upload_processor->processMetaData($metadata);
        $detector = $data_processor->getDetector("-d-");
        $misuse = $data_processor->getMisuse("ex1", $detector, "-p-", "-v-", "-m-");

        $expected_misuse = new Misuse(
            [
                'misuse' => '-m-',
                'project' => '-p-',
                'version' => '-v-',
                'description' => '-desc-',
                'fix_description' => '-fix-desc-',
                'violation_types' => 'superfluous/condition/null_check',
                'file' => '-f-',
                'method' => '-method-',
                'diff_url' => '-diff-',
                'snippets' => [['line' => '273', 'snippet' => '-code-']],
                'patterns' => [['name' => '-p-id-','code' => '-pattern-code-','line' => '1']]
            ],
            [[
                'exp' => 'ex1',
                'project' => '-p-',
                'version' => '-v-',
                'misuse' => '-m-',
                'rank' => '0',
                'custom1' => '-val1-',
                'custom2' => '-val2-',
            ]],
            []);

        self::assertEquals($expected_misuse, $misuse);
    }

}
